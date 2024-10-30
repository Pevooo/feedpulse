using Microsoft.AspNetCore.Identity;

namespace web_api.Models
{
    public class Organization:IdentityUser
    {   
        public string OrgnaizationName { get; set; } = string.Empty;
        public string Describtion { get; set; } = string.Empty;
        public string Country { get; set; }=string.Empty;
        public string City { get; set; }= string.Empty; 
        public IEnumerable<Report> Reports { get; set; }
        public IEnumerable<ORGSocial> ORGSocials { get; set; }
        public List<RefreshToken>? RefreshTokens { get; set; }
    }
}
