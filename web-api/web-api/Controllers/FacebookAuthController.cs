using Api.Core.Features.Facebook.Queries.Models;
using Microsoft.AspNetCore.Mvc;
using web_api.Base;

namespace web_api.Controllers
{
    [Route("api/facebook")]
    [ApiController]
    public class FacebookAuthController : AppControllerBase
    {
        [HttpPost("connect")]
        public async Task<IActionResult> FacebookLogin([FromBody] FacebookAuthQuery query)
        {
            var response = await Mediator.Send(query);
            return NewResult(response);
        }
        [HttpGet("pages")]
        public async Task<IActionResult> GetPages([FromQuery] GetFacebookPageListQuery query)
        {
            var response = await Mediator.Send(query);
            return NewResult(response);
        }
        [HttpPost("unregisteredpages")]
        public async Task<IActionResult> GetUnregisteredPages([FromQuery] GetUnregisteredFacebookPageListQuery query)
        {
            var response = await Mediator.Send(query);
            return NewResult(response);
        }
    }
}
