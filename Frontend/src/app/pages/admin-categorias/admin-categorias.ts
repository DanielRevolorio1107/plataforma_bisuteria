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


  constructor(
    private categoriasService: CategoriasService
  ) {}


  ngOnInit(): void {

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

}