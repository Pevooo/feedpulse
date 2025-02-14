using Api.Core.Features.Authorization.Commands.Models;
using Api.Core.Features.Authorization.Queries.Models;
using Api.Data.AppMetaData;
using Microsoft.AspNetCore.Mvc;
using web_api.Base;

namespace web_api.Controllers
{

    [ApiController]
    public class AuthorizationController : AppControllerBase
    {
        [HttpPost(Router.Authorization.CreateRole)]
        public async Task<IActionResult> Create([FromForm] AddRoleCommand command)
        {
            var response = await Mediator.Send(command);
            return NewResult(response);
        }
        [HttpPut(Router.Authorization.EditRole)]
        public async Task<IActionResult> Edit([FromForm] EditRoleCommand command)
        {
            var response = await Mediator.Send(command);
            return NewResult(response);
        }
        [HttpDelete(Router.Authorization.DeleteRole)]
        public async Task<IActionResult> Delete([FromRoute] int id)
        {
            var response = await Mediator.Send(new DeleteRoleCommand(id));
            return NewResult(response);
        }
        [HttpGet(Router.Authorization.RoleList)]
        public async Task<IActionResult> GetRoleList()
        {
            var response = await Mediator.Send(new GetRoleListQuery());
            return NewResult(response);
        }
        [HttpGet(Router.Authorization.RoleById)]
        public async Task<IActionResult> GetRoleByid([FromRoute] string id)// Get Role By Id
        {
            var response = await Mediator.Send(new GetRoleByIdQuery() { RoleId = id });
            return NewResult(response);
        }
        [HttpGet(Router.Authorization.ManageUserRole)]
        public async Task<IActionResult> ManageUserRoles([FromRoute] string id)// Get Roles For User
        {
            var response = await Mediator.Send(new ManageUserRolesQuery() { UserId = id });
            return NewResult(response);
        }
        [HttpPut(Router.Authorization.UpdateUserRoles)]
        public async Task<IActionResult> UpdateUserRoles([FromBody] UpdateUserRolesCommand command) // Update User's Roles
        {
            var response = await Mediator.Send(command);
            return NewResult(response);
        }

    }
}
