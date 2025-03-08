using Api.Core.Bases;

using Api.Core.Features.Organizations.Commands.Models;
using Api.Data.Entities;
using Api.Service.Abstracts;
using AutoMapper;
using MediatR;

namespace Api.Core.Features.Organizations.Commands.Handler
{
    public class OrganizationCommandHandler : ResponseHandler, IRequestHandler<AddOrganizationCommand, Response<string>>
                            , IRequestHandler<DeleteOrganizationCommand, Response<string>>
    {
        #region Fields
        IOrganizationService _organizationService;
        IMapper _mapper;
        #endregion
        #region Constructor
        public OrganizationCommandHandler(IOrganizationService organizationService, IMapper mapper)
        {
            _organizationService = organizationService;
            _mapper = mapper;
        }
        #endregion
        #region HandleFunctions
        public async Task<Response<string>> Handle(AddOrganizationCommand request, CancellationToken cancellationToken)
        {
            var organization = _mapper.Map<Organization>(request);
            var res = await
              _organizationService.AddOrganizationAsync(organization);
            if (res == "Success")
            {
                return Success(res);
            }
            else
            {
                return BadRequest<string>(res);
            }
        }

        public async Task<Response<string>> Handle(DeleteOrganizationCommand request, CancellationToken cancellationToken)
        {
            var res = await _organizationService.DeleteOrganizationAsync(request.id);
            if (res == "Success")
            {
                return Success("Deleted");
            }
            return NotFound<string>(res);
        }
        #endregion
    }
}
