using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Api.Data.Entities.Identity
{
	public class UserRefershToken
	{
		[Key]
		public int Id { get; set; }
		public string AppUserId { get; set; }
		public string? Token { get; set; }
		public string? RefreshToken { get; set; }
		public string? JwtId { get; set; }
		public bool IsUsed { get; set; }
		public bool IsRevoked { get; set; }
		public DateTime AddedTime { get; set; }
		public DateTime ExpiryDate { get; set; }

		[ForeignKey(nameof(AppUserId))]
		[InverseProperty(nameof(AppUser.UserRefreshTokens))]
		public virtual AppUser? user { get; set; }
	}
}
