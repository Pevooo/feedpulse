import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [RouterLink,RouterOutlet,HttpClientModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent implements OnInit {
  constructor(private http: HttpClient){

  }
  ngOnInit(): void {
    this.fetchDetails();
  }
  public fetchDetails(){
//     this.http.get('https://jsonplaceholder.typicode.com/todos/1').subscribe(
//     (resp:any)=>{
//       console.log(resp);
//     })
// ;
  }
}
