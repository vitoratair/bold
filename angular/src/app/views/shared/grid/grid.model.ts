export interface IGridMenusColumns {
    id: string,
    label: string,
    icon: string,
    is_visible: boolean,
    visibility_data: string | null,
    visibility_data_return: boolean
}
export class GridMenusColumns implements IGridMenusColumns {

    constructor (
        public id: string,
        public label: string,
        public icon: string,
        public is_visible: boolean = true,
        public visibility_data: string | null = null,
        public visibility_data_return: boolean | null = null
    ) {}
}

export interface IGridHttpColumns {
    name: string,
    data: string,
    type: string,
    deep_desc: string | boolean,
    sortable: boolean,
    sort_by: string | null,
    menu: IGridMenusColumns[] | null
  }

export class GridHttpColumns implements IGridHttpColumns {

    constructor (
        public name: string,
        public data: string,
        public type: string = 'text',
        public deep_desc: string | boolean = false,
        public sortable: boolean,
        public sort_by: string,
        public menu: IGridMenusColumns[] | null = null
    ) {}
}


export interface IGridColumns {
    name: string;
    data: string;
    data_api: boolean;
    data_api_field: string | null;
    sortable: boolean;
    sort_by: string | null;
	is_visible: boolean;
    menu: IGridMenusColumns[] | null
  }

export class GridColumns implements IGridColumns {

    constructor (
        public name: string,
        public data: string,
        public data_api_field: string,
        public data_api: boolean = false,
        public sortable: boolean,
        public sort_by: string,
		public is_visible: boolean = true,
        public menu: IGridMenusColumns[] | null = null
    ) {}
}

export interface IGridConfig {
    columns: IGridColumns[];
    limit: number;
    toggleColumns: boolean;
    filter: boolean;
    checkbox: boolean;
}

export class GridConfig implements IGridConfig {

    constructor (
        public columns: IGridColumns[],
        public limit: number = 10,
        public toggleColumns: boolean = true,
        public filter: boolean = true,
        public checkbox: boolean = false,
      ) {}
}

export interface IGridHttpConfig {
    href: string,
    columns: IGridHttpColumns[];
    limit: number;
    toggleColumns: boolean;
    filter: boolean;
    filter_by: string[],
    checkbox: boolean,
}

export class GridHttpConfig implements IGridHttpConfig {

    constructor (
        public href: string,
        public columns: IGridHttpColumns[],
        public limit: number = 10,
        public toggleColumns: boolean = true,
        public filter: boolean = true,
        public filter_by: string[],
        public checkbox: boolean = false,
      ) {}

}
