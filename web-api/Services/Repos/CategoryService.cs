using web_api.Data;
using web_api.Infrastructure;
using web_api.Models;
using web_api.Services.Interfaces;

namespace web_api.Services.Repos
{
    public class CategoryService : BaseRepository<Category>, ICategoryService
    {
        private readonly ApplicationDbContext _context;
        public CategoryService(ApplicationDbContext context) : base(context)
        {
            {
                _context = context;
            }
        }


    }
}
