import {inject, Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, CanActivateFn, Router, RouterStateSnapshot} from '@angular/router';
import { DataHandlerService } from '../service/data-handler.service';

@Injectable({
  providedIn: 'root',
})
class AuthGuard {
  constructor(
    private authService: DataHandlerService,
    private router: Router
  ) {}
  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (this.authService.isAuthenticated()) {
      return true;
    } else {
      this.router.navigate(['/login']);
      return false;
    }
  }
}
export const isAuthGuard: CanActivateFn =  (route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean => {
  return inject(AuthGuard).canActivate(route, state);
}
