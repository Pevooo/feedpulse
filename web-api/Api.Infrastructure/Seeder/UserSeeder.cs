using Api.Data.Entities.Identity;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

namespace Api.Infrastructure.Seeder
{
    public class UserSeeder
    {
        /*
            {
              "fullName": "string",
              "userName": "abdoayman",
              "email": "abdoayman10@gmail.com",
              "password": "Test@123",
              "confirmPassword": "Test@123",
              "country": "string",
              "address": "string",
              "phoneNumber": "string",
              "description": "string"
            }
         
         */
        public static async Task SeedAsync(UserManager<Organization> _userManager)
        {
            var usersCount = await _userManager.Users.CountAsync();
            if (usersCount <= 2)
            {
                var defaultuser = new Organization()
                {
                    UserName = "admin",
                    Email = "admin@project.com",
                    FullName = "JohnAshraf",
                    Country = "Egypt",
                    PhoneNumber = "2121212",
                    Address = "Egypt",
                    EmailConfirmed = true,
                    PhoneNumberConfirmed = true,
                    Description = "testing"

                };
                _ = await _userManager.CreateAsync(defaultuser, "M123_m");
                _ = await _userManager.AddToRoleAsync(defaultuser, "Admin");
            }
        }
    }
}
