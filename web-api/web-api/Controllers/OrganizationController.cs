using Api.Core.Features.Organizations.Commands.Models;
using Api.Data.AppMetaData;
using Microsoft.AspNetCore.Mvc;
using web_api.Base;

namespace web_api.Controllers
{

    [ApiController]
    public class OrganizationController : AppControllerBase
    {
        [HttpPost(Router.Organization.Create)]
        public async Task<IActionResult> Create([FromForm] AddOrganizationCommand command)
        {
            var response = await Mediator.Send(command);
            return NewResult(response);
        }
        [HttpDelete(Router.Organization.Delete)]
        public async Task<IActionResult> Delete([FromRoute] int id)
        {
            var response = await Mediator.Send(new DeleteOrganizationCommand(id));
            return NewResult(response);
        }
    }
}
