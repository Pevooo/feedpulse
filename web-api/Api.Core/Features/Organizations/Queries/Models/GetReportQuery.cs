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
	public class GetReportQuery:IRequest<Response<GetReportResponse>>
	{
		public string page_id {  get; set; }
		public DateTime start_date { get; set; }
		public DateTime end_date { get; set; }
	}
}
