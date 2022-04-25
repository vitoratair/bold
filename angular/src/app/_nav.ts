import { INavData } from '@coreui/angular';

export const navItems: INavData[] = [
  {
    title: true,
    name: 'Data management'
  },
  {
    name: 'Bold',
    url: '/',
    icon: 'icon-puzzle',
    children: [
	  {
        name: 'Movies',
        url: '/admin/movies/',
        icon: 'icon-puzzle'
      },
    ]
  }
];
