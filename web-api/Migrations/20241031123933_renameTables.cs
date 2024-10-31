using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace web_api.Migrations
{
    /// <inheritdoc />
    public partial class renameTables : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "ORGSocialId",
                table: "ORGSocials",
                newName: "OrganizationSocialId");

            migrationBuilder.RenameColumn(
                name: "Describtion",
                table: "AspNetUsers",
                newName: "Description");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "OrganizationSocialId",
                table: "ORGSocials",
                newName: "ORGSocialId");

            migrationBuilder.RenameColumn(
                name: "Description",
                table: "AspNetUsers",
                newName: "Describtion");
        }
    }
}
