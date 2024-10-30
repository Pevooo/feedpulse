using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using web_api.Models;

namespace web_api.Data
{
    public class ApplicationDbContext:IdentityDbContext<Organization>
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext>options):base(options) { }
        
        public DbSet<Organization> Organizations { get; set; }
        public DbSet<Report> Reports { get; set; }
        public DbSet<Category> Categories { get; set; }
        public DbSet<ORGSocial> ORGSocials { get; set; }
    }
}
