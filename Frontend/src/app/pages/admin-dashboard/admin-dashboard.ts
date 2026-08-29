import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../services/auth.service';


@Component({
  selector: 'app-admin-dashboard',
  imports: [RouterLink],
  templateUrl: './admin-dashboard.html',
  styleUrl: './admin-dashboard.css'
})
export class AdminDashboard {

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}


  cerrarSesion(): void {

    this.authService.cerrarSesion();

    this.router.navigate([
      '/admin/login'
    ]);
  }

}