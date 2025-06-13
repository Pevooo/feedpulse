using Api.Core.Bases;

using Api.Data.DTOS;
using MediatR;

namespace Api.Core.Features.Organizations.Queries.Models
{
    public class GetChatReponseQuery : IRequest<Response<ChatResponse>>
    {
        public string page_id { get; set; }
        public DateTime start_date { get; set; }
        public DateTime end_date { get; set; }
        public string question { get; set; }
    }
}
