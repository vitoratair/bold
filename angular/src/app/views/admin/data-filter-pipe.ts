import * as _ from 'lodash';
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'dataFilter'
})
export class DataFilterPipe implements PipeTransform {

  transform(table: any[], query: string, field: string): any {

    if (! query) {
      return table;
    }

    if (field in table[0]) {

      if (field === 'name') {
        return _.filter(table, row => row.name.indexOf(query) > -1);
      }

      if (field === 'ncm') {
        return _.filter(table, row => row.ncm.indexOf(query) > -1);
      }

      if (field === 'description') {
        return _.filter(table, row => row.description.indexOf(query) > -1);
      }

    }

    return table;

  }

}
