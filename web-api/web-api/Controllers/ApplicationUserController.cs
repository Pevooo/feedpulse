using Api.Core.Features.Users.Commands.Models;
using Api.Core.Features.Users.Queries.Models;
using Api.Data.AppMetaData;
using Microsoft.AspNetCore.Mvc;
using web_api.Base;

namespace web_api.Controllers
{
    [ApiController]
    public class ApplicationUserController : AppControllerBase
    {
        [HttpPost(Router.ApplicationUser.Create)]
        public async Task<IActionResult> CreateUser([FromBody] AddUserCommand model)
        {
            var response = await Mediator.Send(model);
            return NewResult(response);
        }
        [HttpGet(Router.ApplicationUser.Paginated)]
        public async Task<IActionResult> Paginated([FromQuery] GetPaginatedListQuery query)
        {
            var response = await Mediator.Send(query);
            return Ok(response);
        }
        [HttpGet(Router.ApplicationUser.GetById)]
        public async Task<IActionResult> GetUserByID([FromRoute] string id)
        {
            return NewResult(await Mediator.Send(new GetUserByIdQuery { Id = id }));
        }
        [HttpPut(Router.ApplicationUser.Edit)]
        public async Task<IActionResult> EditUser([FromBody] EditUserCommand model)
        {
            var response = await Mediator.Send(model);
            return NewResult(response);
        }
        [HttpDelete(Router.ApplicationUser.Delete)]
        public async Task<IActionResult> Delete([FromRoute] DeleteUserCommand model)
        {
            var response = await Mediator.Send(model);
            return NewResult(response);
        }
        [HttpPut(Router.ApplicationUser.ChangePassword)]
        public async Task<IActionResult> ChangePassword([FromBody] ChangeUserPasswordCommand model)
        {
            var response = await Mediator.Send(model);
            return NewResult(response);
        }
    }
}
