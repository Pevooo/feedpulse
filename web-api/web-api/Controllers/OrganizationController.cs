using Api.Core.Features.Organizations.Commands.Models;
using Api.Core.Features.Organizations.Queries.Models;
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
        [HttpPost(Router.Organization.GetById)]
        public async Task<IActionResult> GetById([FromRoute] int id)
        {
            var response = await Mediator.Send(new GetOrganizationQuery { OrganizationId = id });
            return NewResult(response);
        }
        [HttpPost(Router.Organization.GetList)]
        public async Task<IActionResult> GetList([FromForm] GetOrganizationListQuery query)
        {
            var response = await Mediator.Send(query);
            return NewResult(response);
        }
        [HttpPost(Router.Organization.Status)]
        public async Task<IActionResult> GetStatus([FromBody] GetOrganizationStatusQuery query)
        {
            var response = await Mediator.Send(query);
            return NewResult(response);
        }
    }
}
