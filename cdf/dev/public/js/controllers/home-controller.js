(function(app) {
	app.controller('HomeController', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
		this.cancerTypes = [
				"GBM",
				"THCA",
				"LAML",
				"HNSC",
				"LUAD",
				"UCEC",
				"KIRC",
				"SARC",
				];
		this.tissueTypes = ["healthy", "unhealthy"];
		this.selectedCancerTypes = [];
		this.selectedTissueTypes = [];
		this.request = () => {
			var object = {
				status: "pending", 
				data: {}, 
				request:{
					cancerTypes: this.selectedCancerTypes, 
					tissueTypes: this.selectedTissueTypes
				}
			};
			request(object);
			this.results.push(object);
		};		
		this.results = [];		

		function request(handle) {
			let request = JSON.stringify(handle.request);
			$http.get(`http://localhost:8000/validate/${request}`, {timeout: 3*60*1000})
			.then((response) => {
				handle.data = response.data;
				handle.status = "finished";
			})
			.catch((error) => {
				handle.data = error;
				handle.status = "error";			
			});
		}
	}]);
})(cdf);
