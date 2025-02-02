using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

namespace Api.Infrastructure.Seeder
{
    public static class RoleSeeder
    {
        public static async Task SeedAsync(RoleManager<IdentityRole> _roleManager)
        {
            var rolesCount = await _roleManager.Roles.CountAsync();
            if (rolesCount <= 0)
            {

                _ = await _roleManager.CreateAsync(new IdentityRole()
                {
                    Name = "Admin"
                });
                _ = await _roleManager.CreateAsync(new IdentityRole()
                {
                    Name = "User"
                });
            }
        }
    }
}
