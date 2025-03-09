using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Api.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class correctIdType : Migration
    {
		/// <inheritdoc />
		protected override void Up(MigrationBuilder migrationBuilder)
		{
			migrationBuilder.DropPrimaryKey(name: "PK_Reports", table: "Reports");
			migrationBuilder.DropPrimaryKey(name: "PK_Organizations", table: "Organizations");

			migrationBuilder.DropColumn(name: "Id", table: "Reports");
			migrationBuilder.DropColumn(name: "Id", table: "Organizations");

			migrationBuilder.AddColumn<int>(
				name: "Id",
				table: "Reports",
				nullable: false)
				.Annotation("SqlServer:Identity", "1, 1");

			migrationBuilder.AddColumn<int>(
				name: "Id",
				table: "Organizations",
				nullable: false)
				.Annotation("SqlServer:Identity", "1, 1");

			migrationBuilder.AddPrimaryKey("PK_Reports", "Reports", "Id");
			migrationBuilder.AddPrimaryKey("PK_Organizations", "Organizations", "Id");
		}

		protected override void Down(MigrationBuilder migrationBuilder)
		{
			migrationBuilder.DropPrimaryKey(name: "PK_Reports", table: "Reports");
			migrationBuilder.DropPrimaryKey(name: "PK_Organizations", table: "Organizations");

			migrationBuilder.DropColumn(name: "Id", table: "Reports");
			migrationBuilder.DropColumn(name: "Id", table: "Organizations");

			migrationBuilder.AddColumn<string>(
				name: "Id",
				table: "Reports",
				type: "nvarchar(450)",
				nullable: false);

			migrationBuilder.AddColumn<string>(
				name: "Id",
				table: "Organizations",
				type: "nvarchar(450)",
				nullable: false);

			migrationBuilder.AddPrimaryKey("PK_Reports", "Reports", "Id");
			migrationBuilder.AddPrimaryKey("PK_Organizations", "Organizations", "Id");
		}
	}
}
