using Api.Data.Entities.Identity;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Api.Core.Features.Organizations.Queries.Responses
{
	public class GetOrganizationResponse
	{
		public string Name { get; set; }
		public string FacebookId { get; set; }
		public string Description { get; set; }
		public string? PageAccessToken { get; set; }
	}
}
