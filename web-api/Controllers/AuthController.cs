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
		[HttpPost("register")]
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
		[HttpPost("login")]
		public async Task<IActionResult> LoginAsync([FromBody] LoginDto model)
		{
			var result = await _authService.LoginAsync(model);

			if (!result.IsAuthenticated)
				return BadRequest(result.Message);

			if (!string.IsNullOrEmpty(result.RefreshToken))
				SetRefreshTokenInCookie(result.RefreshToken, result.RefreshTokenExpiration);

			return Ok(result);
		}

		[HttpGet("refreshToken")]
		public async Task<IActionResult> RefreshToken()
		{
			var refreshToken = Request.Cookies["refreshToken"];

			var result = await _authService.RefreshTokenAsync(refreshToken);

			if (!result.IsAuthenticated)
				return BadRequest(result);

			SetRefreshTokenInCookie(result.RefreshToken, result.RefreshTokenExpiration);

			return Ok(result);
		}
		[HttpPost("revokeToken")]
		public async Task<IActionResult> RevokeToken([FromBody] string token)
		{
			if (string.IsNullOrEmpty(token))
				token = Request.Cookies["refreshToken"];

			if (string.IsNullOrEmpty(token))
				return BadRequest("Token is required!");

			var result = await _authService.RevokeTokenAsync(token);

			if (!result)
				return BadRequest("Token is invalid!");

			return Ok();
		}
		private void SetRefreshTokenInCookie(string refreshToken, DateTime expires)
		{
			var cookieOptions = new CookieOptions
			{
				HttpOnly = true,
				Expires = expires.ToLocalTime(),
				Secure = true,
				IsEssential = true,
				SameSite = SameSiteMode.None
			};

			Response.Cookies.Append("refreshToken", refreshToken.ToString(), cookieOptions);
		}
	}
}
