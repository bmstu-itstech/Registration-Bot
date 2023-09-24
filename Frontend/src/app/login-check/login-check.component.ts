import { Component } from '@angular/core';
import { Router } from '@angular/router';
import {DataHandlerService} from "../service/data-handler.service";

@Component({
  selector: 'app-login-check',
  templateUrl: './login-check.component.html',
  styleUrls: ['./login-check.component.css']
})
export class LoginCheckComponent {
  username: string = '';
  password: string = '';
  constructor(private router: Router, private DataHandlerService: DataHandlerService) { }
  login() {
    if (this.username === 'user' && this.password === 'password') {
      this.DataHandlerService.setCookie('authToken', 'yourAuthTokenValue', 1);
      this.router.navigate(['/']);
    } else {
      alert('Ошибка авторизации. Проверьте логин и пароль.');
    }
  }
}
