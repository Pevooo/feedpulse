using Api.Core.Bases;
using Api.Core.Features.Organizations.Queries.Responses;
using MediatR;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Api.Core.Features.Organizations.Queries.Models
{
	public class GetOrganizationListQuery:IRequest<Response<List<GetOrganizationResponse>>>
	{
		public string UserId { get; set; }
	}
}
