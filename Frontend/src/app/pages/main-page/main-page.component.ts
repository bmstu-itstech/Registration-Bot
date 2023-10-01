import {Component, OnInit} from '@angular/core';
import { Router } from '@angular/router';
import {DataHandlerService} from "../../service/data-handler.service";

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent implements OnInit{
  constructor(
    private router: Router,
    private cookieService: DataHandlerService
  ) { }
  ngOnInit(): void {
  }
  onTryClick(): void {
    const isAuthenticated = this.cookieService.getCookie('authToken');
    if (isAuthenticated) {
      this.router.navigate(['/list']);
    } else {
      this.router.navigate(['/its-id']);
    }
  }
}
