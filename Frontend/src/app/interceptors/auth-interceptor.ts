import { inject } from '@angular/core';

import {
  HttpErrorResponse,
  HttpInterceptorFn
} from '@angular/common/http';

import {
  Router
} from '@angular/router';

import {
  catchError,
  throwError
} from 'rxjs';

import {
  AuthService
} from '../services/auth.service';


export const authInterceptor: HttpInterceptorFn =
  (req, next) => {

    const authService =
      inject(AuthService);

    const router =
      inject(Router);


    const esBackend =
      req.url.startsWith(
        'http://127.0.0.1:8000/'
      );


    if (!esBackend) {

      return next(req);

    }


    const token =
      authService.obtenerToken();


    if (!token) {

      return next(req);

    }


    if (!authService.estaAutenticado()) {

      return next(req);

    }


    const requestConToken =
      req.clone({

        setHeaders: {

          Authorization:
            `Bearer ${token}`

        }

      });


    return next(
      requestConToken
    ).pipe(

      catchError(
        (error: HttpErrorResponse) => {

          if (error.status === 401) {

            authService.cerrarSesion();

            router.navigate([
              '/admin/login'
            ]);

          }


          return throwError(
            () => error
          );
        }
      )

    );
  };