import { Component, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import {
  Categoria,
  CategoriasService
} from '../../services/categorias.service';


@Component({
  selector: 'app-admin-categorias',
  imports: [RouterLink],
  templateUrl: './admin-categorias.html',
  styleUrl: './admin-categorias.css'
})
export class AdminCategorias implements OnInit {

  categorias = signal<Categoria[]>([]);

  cargando = signal(true);
  error = signal('');
  mensaje = signal('');


  constructor(
    private categoriasService: CategoriasService
  ) {}


  ngOnInit(): void {
    this.cargarCategorias();
  }


  cargarCategorias(): void {

    this.categoriasService.obtenerTodasAdmin().subscribe({

      next: (categorias) => {
        this.categorias.set(categorias);
        this.cargando.set(false);
      },

      error: () => {
        this.error.set(
          'No se pudieron cargar las categorías'
        );

        this.cargando.set(false);
      }

    });
  }


  desactivar(categoria: Categoria): void {

    this.error.set('');
    this.mensaje.set('');

    this.categoriasService
      .desactivarCategoria(categoria.id_categoria)
      .subscribe({

        next: () => {

          this.mensaje.set(
            'Categoría desactivada correctamente'
          );

          this.cargarCategorias();
        },

        error: (error) => {

          this.error.set(
            error.error?.detail ||
            'No se pudo desactivar la categoría'
          );
        }

      });
  }


  activar(categoria: Categoria): void {

    this.error.set('');
    this.mensaje.set('');

    this.categoriasService
      .activarCategoria(categoria.id_categoria)
      .subscribe({

        next: () => {

          this.mensaje.set(
            'Categoría activada correctamente'
          );

          this.cargarCategorias();
        },

        error: (error) => {

          this.error.set(
            error.error?.detail ||
            'No se pudo activar la categoría'
          );
        }

      });
  }

}