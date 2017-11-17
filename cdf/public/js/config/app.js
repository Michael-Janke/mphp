var cdf = angular.module('cdf', ['ngMaterial', 'ngAnimate', 'ngMessages', 'ngAria', 'ui.router']);

(function(app) {
    app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise('/');

        $stateProvider.state('home', {
            url: '/',
            templateUrl: 'partials/home-partial.html',
            controller: 'HomeController',
            controllerAs: 'ctrl'
        })

        .state('about', {
            url: '/about',
            templateUrl: 'partials/about-partial.html',
            controller: 'AboutController'
        });
    }]);
})(cdf);
