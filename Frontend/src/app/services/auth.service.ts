import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface LoginRequest {
  usuario: string;
  password: string;
}


export interface TokenResponse {
  access_token: string;
  token_type: string;
}


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private http = inject(HttpClient);

  private apiUrl =
    'http://127.0.0.1:8000/auth/login';


  login(
    datos: LoginRequest
  ): Observable<TokenResponse> {

    return this.http.post<TokenResponse>(
      this.apiUrl,
      datos
    );
  }


  guardarToken(token: string): void {
    localStorage.setItem(
      'admin_token',
      token
    );
  }


  obtenerToken(): string | null {
    return localStorage.getItem(
      'admin_token'
    );
  }


  cerrarSesion(): void {
    localStorage.removeItem(
      'admin_token'
    );
  }


  estaAutenticado(): boolean {
    return this.obtenerToken() !== null;
  }

}