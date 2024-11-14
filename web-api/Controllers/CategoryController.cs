using Microsoft.AspNetCore.Mvc;
using web_api.Helpers;
using web_api.UnitOfWork;

namespace web_api.Controllers
{
    [ApiController]
    public class CategoryController : ControllerBase
    {
        private readonly IUnitOfWork _unitOfWork;

        public CategoryController(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }
        [HttpGet(Routes.CategoryRouting.List)]
        public IActionResult GetAll()
        {
            return Ok(_unitOfWork.CategoryService.GetAll());
        }
    }
}
