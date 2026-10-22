using BookStore.Api.Models;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;

namespace BookStore.Api.Data
{
    public static class DbSeeder
    {
        public static void SeedBooksFromJson(AppDbContext context, string jsonPath)
        {
            // Only seed if there are no books in the database
            if (!context.Books.Any())
            {
                if (File.Exists(jsonPath))
                {
                    var json = File.ReadAllText(jsonPath);
                    var books = JsonSerializer.Deserialize<List<Book>>(json);

                    if (books != null)
                    {
                        context.Books.AddRange(books);
                        context.SaveChanges();
                        Console.WriteLine($"Seeded {books.Count} books from JSON.");
                    }
                }
            }
        }

        public static void SeedAdmin(AppDbContext context, IHostEnvironment environment)
        {
            if (context.Users.Any(u => u.Username == "admin"))
                return;

            // One-time bootstrap credentials: set BOOKSTORE_ADMIN_PASSWORD (and
            // optionally BOOKSTORE_ADMIN_EMAIL) for the first start; unset the
            // variables afterwards and change the password in the app.
            var bootstrapPassword = Environment.GetEnvironmentVariable("BOOKSTORE_ADMIN_PASSWORD");
            var bootstrapEmail = Environment.GetEnvironmentVariable("BOOKSTORE_ADMIN_EMAIL") ?? "admin@bookstore.com";

            if (string.IsNullOrEmpty(bootstrapPassword))
            {
                if (environment.IsDevelopment())
                {
                    bootstrapPassword = "1234"; // local development default only
                    Console.WriteLine("[Seeder] Development: created admin/1234. Never deploy this combination.");
                }
                else
                {
                    Console.WriteLine("[Seeder] Refusing to seed 'admin': BOOKSTORE_ADMIN_PASSWORD is not set. " +
                                      "Set it once for first login, then remove the variable.");
                    return;
                }
            }

            context.Users.Add(new User
            {
                Username = "admin",
                PasswordHash = BCrypt.Net.BCrypt.HashPassword(bootstrapPassword),
                Role = "Admin",
                FirstName = "Sistem",
                LastName = "Yöneticisi",
                Email = bootstrapEmail
            });
            context.SaveChanges();
        }

        public static void SyncStockStatus(AppDbContext context)
        {
            var zeroStockBooks = context.Books.Where(b => b.StockQuantity <= 0 && b.IsActive).ToList();
            foreach (var book in zeroStockBooks)
            {
                book.IsActive = false;
            }
            context.SaveChanges();
        }
    }
}
