using Api.Core.Bases;
using Api.Core.Features.Organizations.Queries.Models;
using Api.Core.Features.Organizations.Queries.Responses;
using Api.Service.Abstracts;
using AutoMapper;
using MediatR;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Api.Core.Features.Organizations.Queries.Handler
{
	
	public class OrganizationQueryHandler: ResponseHandler, IRequestHandler<GetOrganizationListQuery, Response<List<GetOrganizationResponse>>>
							, IRequestHandler<GetOrganizationQuery, Response<GetOrganizationResponse>>
	{
		#region Fields
		IOrganizationService _organizationService;
		IMapper _mapper;
		#endregion
		#region Constructor
		public OrganizationQueryHandler(IOrganizationService organizationService, IMapper mapper)
		{
			_organizationService = organizationService;
			_mapper = mapper;
		}
		#endregion
		#region HandleFunctions
		public async Task<Response<List<GetOrganizationResponse>>> Handle(GetOrganizationListQuery request, CancellationToken cancellationToken)
		{
			var organizations = await _organizationService.GetOrganizationsByUseridAsync(request.UserId);
			var response= organizations.Select(o=>new  GetOrganizationResponse
			{
				Name=o.Name,
				Description=o.Description,
				FacebookId=o.FacebookId,
				PageAccessToken=o.PageAccessToken
			}).ToList();

			return Success(response);
		}

		public async Task<Response<GetOrganizationResponse>> Handle(GetOrganizationQuery request, CancellationToken cancellationToken)
		{
			var organization = await _organizationService.GetOrganizationByIdAsync(request.OrganizationId);
			var response = new GetOrganizationResponse
			{
				Name = organization.Name,
				Description = organization.Description,
				FacebookId = organization.FacebookId,
				PageAccessToken = organization.PageAccessToken
			};
			return Success(response);
		}
		#endregion
	}
}
