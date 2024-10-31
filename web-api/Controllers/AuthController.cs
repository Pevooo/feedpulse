using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using web_api.Dtos.Authentication;
using web_api.Services.Interfaces;

namespace web_api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly IAuth _authService;
        public AuthController(IAuth authservice)
        {
            _authService = authservice;
        }
        [HttpPost]
        public async Task<IActionResult> Register([FromBody] RegisterDto model)
        {
            if (!ModelState.IsValid) { return BadRequest("Check Inputs"); }
            var AuthResult = await _authService.RegisterAsync(model);
            if (!AuthResult.IsAuthenticated)
            {
                return BadRequest(AuthResult.Message);
            }
            return Ok(AuthResult);
        }
    }
}
