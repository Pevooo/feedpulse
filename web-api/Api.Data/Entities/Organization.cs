using Api.Data.Entities.Identity;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Api.Data.Entities
{
    public class Organization
	{
		public string Id { get; set; }
		public string Name { get; set; }
		public string Description { get; set; }

		// Relation with User
		public string UserId { get; set; }
		[ForeignKey(nameof(UserId))]
		[InverseProperty(nameof(AppUser.Organizations))]
		public virtual AppUser? user { get; set; }

		// Relation with OrganizationAccessToken
		[InverseProperty(nameof(OrganizationAccessToken.Organization))]
		public virtual ICollection<OrganizationAccessToken> Tokens { get; set; }



	}
}
