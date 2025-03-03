using Api.Core.Bases;

using Api.Core.Features.Organizations.Commands.Models;
using Api.Data.Entities;
using Api.Service.Abstracts;
using AutoMapper;
using MediatR;

namespace Api.Core.Features.Organizations.Commands.Handler
{
    public class OrganizationCommandHandler : ResponseHandler, IRequestHandler<AddOrganizationCommand, Response<string>>
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
        public Task<Response<string>> Handle(AddOrganizationCommand request, CancellationToken cancellationToken)
        {
            _ = _mapper.Map<Organization>(request);
            throw new NotImplementedException();
        }
        #endregion
    }
}
