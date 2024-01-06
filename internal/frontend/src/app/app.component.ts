import { Component } from '@angular/core';
import {ActivatedRoute, NavigationEnd, Router} from "@angular/router";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';
  routerOutletName: string = '';
  constructor(private router: Router, private activatedRoute: ActivatedRoute) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        const childRoute = this.activatedRoute.firstChild;
        if (childRoute) {
          this.routerOutletName = childRoute.routeConfig?.path || '';
        }
      }
    });
  }
  getActiveRouteName(): string {
    return this.routerOutletName;
  }
}
