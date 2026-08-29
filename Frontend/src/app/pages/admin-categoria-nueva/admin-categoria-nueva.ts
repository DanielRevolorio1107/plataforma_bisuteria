import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import {
  CategoriaCreate,
  CategoriasService
} from '../../services/categorias.service';


@Component({
  selector: 'app-admin-categoria-nueva',
  imports: [
    FormsModule,
    RouterLink
  ],
  templateUrl: './admin-categoria-nueva.html',
  styleUrl: './admin-categoria-nueva.css'
})
export class AdminCategoriaNueva {

  nombre = '';
  descripcion = '';

  guardando = signal(false);
  error = signal('');


  constructor(
    private categoriasService: CategoriasService,
    private router: Router
  ) {}


  guardarCategoria(): void {

    if (!this.nombre.trim()) {

      this.error.set(
        'El nombre de la categoría es obligatorio'
      );

      return;
    }


    const categoria: CategoriaCreate = {

      nombre: this.nombre.trim(),

      descripcion:
        this.descripcion.trim() || null

    };


    this.guardando.set(true);
    this.error.set('');


    this.categoriasService.crearCategoria(
      categoria
    ).subscribe({

      next: () => {

        this.router.navigate([
          '/admin/categorias'
        ]);

      },

      error: (error) => {

        this.guardando.set(false);

        this.error.set(
          error.error?.detail ||
          'No se pudo crear la categoría'
        );

      }

    });
  }

}