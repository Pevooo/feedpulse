using EntityFrameworkCore.EncryptColumn.Attribute;
using Microsoft.AspNetCore.Identity;
using System.ComponentModel.DataAnnotations.Schema;

namespace Api.Data.Entities.Identity
{
    public class AppUser : IdentityUser
    {
        public string FullName { get; set; }
        public string? Address { get; set; }
        public string? Country { get; set; }
        public string Photo { get; set; }
        [EncryptColumn]
        public string? Code { get; set; }

        [InverseProperty(nameof(UserRefershToken.Organization))]
        public virtual ICollection<UserRefershToken> UserRefreshTokens { get; set; }
    }
}
