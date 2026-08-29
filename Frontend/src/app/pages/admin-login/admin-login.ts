import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';


@Component({
  selector: 'app-admin-login',
  imports: [FormsModule],
  templateUrl: './admin-login.html',
  styleUrl: './admin-login.css'
})
export class AdminLogin {

  usuario = '';
  password = '';

  cargando = signal(false);
  error = signal('');


  constructor(
    private authService: AuthService,
    private router: Router
  ) {}


  iniciarSesion(): void {

    if (
      !this.usuario.trim() ||
      !this.password.trim()
    ) {
      this.error.set(
        'Ingresa usuario y contraseña'
      );

      return;
    }


    this.cargando.set(true);
    this.error.set('');


    this.authService.login({

      usuario: this.usuario,
      password: this.password

    }).subscribe({

      next: (respuesta) => {

        this.authService.guardarToken(
          respuesta.access_token
        );

        this.router.navigate([
          '/admin'
        ]);
      },

      error: () => {

        this.cargando.set(false);

        this.error.set(
          'Usuario o contraseña incorrectos'
        );
      }

    });
  }

}