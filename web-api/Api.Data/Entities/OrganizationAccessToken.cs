using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Api.Data.Entities
{
    public class OrganizationAccessToken
    {
        public string Id { get; set; }
        public string Value { get; set; }
        public DateTime ExpiresAt { get; set; }

        public string OrganizationId { get; set; }

        [ForeignKey(nameof(OrganizationId))]
        [InverseProperty(nameof(Organization.Tokens))]
        public virtual Organization? Organization { get; set; }
    }
}
