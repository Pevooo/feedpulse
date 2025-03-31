using Api.Core.Bases;
using Api.Core.Features.Facebook.Queries.Responses;
using MediatR;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Api.Core.Features.Facebook.Queries.Models
{
    public class GetUnregisteredFacebookPageListQuery : IRequest<Response<List<SingleFacebookPageResponse>>>
    {
        public string AccessToken { get; set; }
    }
}
