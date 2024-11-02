using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using web_api.Data;

namespace web_api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CategoryController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public CategoryController(ApplicationDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public IActionResult getall()
        {

            return Ok(_context.Categories.ToList());
        }
    }
}
