import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/IndexPage.vue') }],
  },
  {
    path: '/trips',
    component: () => import('layouts/MainLayout.vue'),    
    children: [
      { path: '', component: () => import('pages/TripsPage.vue') },
      {
        path: ':id',
        component: () => import('pages/TripDetailPage.vue'),
        props: true,
        children: [
          {
            path: 'steps/:stepId',
            component: () => import('components/TripDetail/StepDetail.vue'),
            props: true
          }
        ]
      },
    ],
  }, 
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
