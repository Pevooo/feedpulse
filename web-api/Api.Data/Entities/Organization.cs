using Api.Data.Entities.Identity;
using System.ComponentModel.DataAnnotations.Schema;

namespace Api.Data.Entities
{
    public class Organization
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string FacebookId { get; set; }
        public string Description { get; set; }
        public string? PageAccessToken { get; set; }

        // Relation with User
        public string UserId { get; set; }
        [ForeignKey(nameof(UserId))]
        [InverseProperty(nameof(AppUser.Organizations))]
        public virtual AppUser? user { get; set; }



    }
}
