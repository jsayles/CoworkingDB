Directory::Application.routes.draw do
  resources :places
  resources :spaces do
    member do
      get 'geocode'
    end
  end

  root :to => "directory#index"
end
