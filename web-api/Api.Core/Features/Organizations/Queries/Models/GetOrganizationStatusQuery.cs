using Api.Core.Bases;
using Api.Core.Features.Organizations.Queries.Responses;
using MediatR;

namespace Api.Core.Features.Organizations.Queries.Models
{
    public class GetOrganizationStatusQuery : IRequest<Response<OrganizationStatusResponse>>
    {
        public string FacebookId { get; set; }
        public DateTime start_date { get; set; }
        public DateTime end_date { get; set; }

    }
}
