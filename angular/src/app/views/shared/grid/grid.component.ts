import { Component, AfterViewInit, Input, Output, OnInit, ViewChild, OnChanges, EventEmitter, ViewEncapsulation, ChangeDetectionStrategy } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import {SelectionModel} from '@angular/cdk/collections';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { IGridConfig, IGridMenusColumns } from './grid.model';



@Component({
    selector: 'app-grid',
    styleUrls: ['grid.component.scss'],
    templateUrl: 'grid.component.html',
    encapsulation: ViewEncapsulation.None,
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class GridComponent implements OnChanges, AfterViewInit  {
    @Input() rows: any;
    @Input() gridConfig: IGridConfig;
    @Output() rowClick = new EventEmitter();

	displayedColumns: string[] = [];
    public dataSource;
    public selection;

    @ViewChild(MatPaginator) paginator: MatPaginator;
    @ViewChild(MatSort) sort: MatSort;

	constructor() {}

	ngAfterViewInit() {
        this.dataSource = new MatTableDataSource(this.rows);
        this.displayedColumns = this.gridConfig.columns.filter(item => item.is_visible).map(function (item) {return item.data; });
        this.dataSource.sort = this.sort;
        this.dataSource.paginator = this.paginator;
        this.selection = new SelectionModel<any>(true, []);
	}

    ngOnChanges() {
        this.ngAfterViewInit();
    }

    public onSelect(selected: any) {
        this.rowClick.emit(selected);
    }

    public menuEventClick(id: string, row: any) {
        this.rowClick.emit({'id': id, 'row': row});
    }

    isColumnVisible(name: string) {
        return this.displayedColumns.findIndex(col => col === name) > 0;
    }

    /** Whether the number of selected elements matches the total number of rows. */
    isAllSelected() {
        const numSelected = this.selection.selected.length;
        const numRows = this.dataSource.data.length;
        return numSelected === numRows;
    }

    /** Selects all rows if they are not all selected; otherwise clear selection. */
    masterToggle() {
        this.isAllSelected() ?
            this.selection.clear() :
            this.dataSource.data.forEach(row => this.selection.select(row));
    }

    /** The label for the checkbox on the passed row */
    checkboxLabel(row?: any): string {
        if (!row) {
            return `${this.isAllSelected() ? 'select' : 'deselect'} all`;
        }
        return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.position + 1}`;
    }

    columnClick(name: string) {
        const colIndex = this.displayedColumns.findIndex(col => col === name);

        if (colIndex > 0) {
          // column is currently shown in the table, so we remove it
          this.displayedColumns.splice(colIndex, 1);
        } else {
          // column is not in the table, so we add it
          this.displayedColumns.push(name);
        }
    }


    rowEmit(row: any) {
        this.rowClick.emit({'row': row});
    }

    applyFilter(event: Event) {
        const filterValue = (event.target as HTMLInputElement).value;
        this.dataSource.filter = filterValue.trim().toLowerCase();
    }

    public showMenuItem(menu: IGridMenusColumns, row: any) {
      if (menu.is_visible) {
        return true;
      }

      if (row === undefined) {
        return false;
      }

      const visibility_data = row[menu.visibility_data];
      const expected_result = menu.visibility_data_return;

      return visibility_data === expected_result;

    }

}
