using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

using BookStore.Api.Data;
using BookStore.Api.Services;
using Microsoft.EntityFrameworkCore;


var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers().AddJsonOptions(x => x.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles);
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

// --- JWT secret validation ---
// Outside Development the app refuses to start without a real, non-placeholder
// signing secret (set Jwt__Key env var or `dotnet user-secrets set Jwt:Key ...`).
var jwtKey = builder.Configuration["Jwt:Key"];
var insecurePlaceholders = new[] { "CHANGE_ME_SET_VIA_Jwt__Key" };
// Block reuse of the historically leaked signing key without re-committing its
// literal bytes: compare SHA-256 (uppercase hex) of the configured key.
var legacyLeakedKeyHash = "5E2D66E8252D6451ADE9214DAEC219286B46C6595F79E98B5C89F2FA5B4DA1E2";
if (!string.IsNullOrWhiteSpace(jwtKey) &&
    Convert.ToHexString(System.Security.Cryptography.SHA256.HashData(Encoding.UTF8.GetBytes(jwtKey))) == legacyLeakedKeyHash)
    throw new InvalidOperationException("Jwt:Key matches the historically leaked value; rotate it (see README).");
if (!builder.Environment.IsDevelopment() &&
    (string.IsNullOrWhiteSpace(jwtKey) || jwtKey.Length < 32 || insecurePlaceholders.Contains(jwtKey)))
{
    throw new InvalidOperationException(
        "Jwt:Key is missing, shorter than 32 chars, or a known placeholder. " +
        "Provide a unique secret via the Jwt__Key environment variable or user-secrets.");
}

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey!))
        };
    });

builder.Services.AddAuthorization();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.AddSecurityDefinition("Bearer", new Microsoft.OpenApi.Models.OpenApiSecurityScheme
    {
        Name = "Authorization",
        Type = Microsoft.OpenApi.Models.SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT",
        In = Microsoft.OpenApi.Models.ParameterLocation.Header,
        Description = "Bearer {token} yaz?p token? yap??t?r"
    });

    c.AddSecurityRequirement(new Microsoft.OpenApi.Models.OpenApiSecurityRequirement
    {
        {
            new Microsoft.OpenApi.Models.OpenApiSecurityScheme
            {
                Reference = new Microsoft.OpenApi.Models.OpenApiReference
                {
                    Type = Microsoft.OpenApi.Models.ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            new string[] {}
        }
    });
});
builder.Services.Configure<BookStore.Api.Models.EmailSettings>(builder.Configuration.GetSection("EmailSettings"));
builder.Services.AddScoped<IEmailService, EmailService>();
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddMemoryCache();

var corsOrigins = builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>()
    ?? new[] { "http://localhost:5173" };

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins(corsOrigins)
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.Migrate(); // Tabloları otomatik oluşturur/günceller
    DbSeeder.SeedAdmin(db, app.Environment);
    DbSeeder.SeedBooksFromJson(db, "books_data_v2.json");
    DbSeeder.SyncStockStatus(db);
}

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseDefaultFiles();
app.UseStaticFiles();

app.UseCors("AllowFrontend");

app.UseAuthentication();

app.UseAuthorization();

app.MapControllers();
app.MapFallbackToFile("index.html");

app.Run();
