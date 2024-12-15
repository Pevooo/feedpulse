import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { inject } from '@angular/core';
// import{ReactiveFormsModule}from '@angular/forms';
import { FormBuilder}from '@angular/forms';
import{FormGroup}from '@angular/forms';
import{Validators} from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
@Component({
  selector: 'app-login',
  standalone: true,
  imports:[ReactiveFormsModule,RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit {
authService =inject(AuthService);
loginform!:FormGroup;
fb=inject(FormBuilder);
login(){
  this.authService.login(this.loginform.value).subscribe((resp)=>
{
console.log(resp);
})
}
ngOnInit(): void {
this.loginform=this.fb.group({
  email:['',[Validators.required,Validators.email]],
    password:['',Validators.required]
});
}


}
