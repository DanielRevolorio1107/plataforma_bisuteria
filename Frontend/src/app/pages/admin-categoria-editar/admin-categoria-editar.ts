import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  ActivatedRoute,
  Router,
  RouterLink
} from '@angular/router';

import {
  CategoriaUpdate,
  CategoriasService
} from '../../services/categorias.service';


@Component({
  selector: 'app-admin-categoria-editar',
  imports: [
    FormsModule,
    RouterLink
  ],
  templateUrl: './admin-categoria-editar.html',
  styleUrl: './admin-categoria-editar.css'
})
export class AdminCategoriaEditar implements OnInit {

  idCategoria = 0;

  nombre = '';
  descripcion = '';

  cargando = signal(true);
  guardando = signal(false);
  error = signal('');


  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private categoriasService: CategoriasService
  ) {}


  ngOnInit(): void {

    this.idCategoria = Number(
      this.route.snapshot.paramMap.get('id')
    );

    this.categoriasService.obtenerTodasAdmin().subscribe({

      next: (categorias) => {

        const categoria = categorias.find(
          item =>
            item.id_categoria === this.idCategoria
        );

        if (!categoria) {

          this.error.set(
            'La categoría no existe'
          );

          this.cargando.set(false);

          return;
        }

        this.nombre = categoria.nombre;
        this.descripcion =
          categoria.descripcion || '';

        this.cargando.set(false);
      },

      error: () => {

        this.error.set(
          'No se pudo cargar la categoría'
        );

        this.cargando.set(false);
      }

    });
  }


  guardarCategoria(): void {

    if (!this.nombre.trim()) {

      this.error.set(
        'El nombre es obligatorio'
      );

      return;
    }


    const categoria: CategoriaUpdate = {

      nombre: this.nombre.trim(),

      descripcion:
        this.descripcion.trim() || null
    };


    this.guardando.set(true);
    this.error.set('');


    this.categoriasService.actualizarCategoria(
      this.idCategoria,
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
          'No se pudo actualizar la categoría'
        );
      }

    });
  }

}