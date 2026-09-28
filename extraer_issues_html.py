System.InvalidOperationException: The association between entity types 'Consultor' and 'CelulaMiembro' has been severed, but the relationship is either marked as required or is implicitly required because the foreign key is not nullable. If the dependent/child entity should be deleted when a required relationship is severed, configure the relationship to use cascade deletes. Consider using 'DbContextOptionsBuilder.EnableSensitiveDataLogging' to see the key values.
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.InternalEntityEntry.HandleConceptualNulls(Boolean sensitiveLoggingEnabled, Boolean force, Boolean isCascadeDelete)
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.InternalEntityEntry.HandleNullForeignKey(IProperty property, Boolean setModified, Boolean isCascadeDelete)
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.InternalEntityEntry.SetProperty(IPropertyBase propertyBase, Object value, Boolean isMaterialization, Boolean setModified, Boolean isCascadeDelete, CurrentValueType valueType)
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.InternalEntityEntry.SetProperty(IPropertyBase propertyBase, Object value, Boolean isMaterialization, Boolean setModified, Boolean isCascadeDelete)
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.InternalEntityEntry.set_Item(IPropertyBase propertyBase, Object value)
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.NavigationFixer.ConditionallyNullForeignKeyProperties(InternalEntityEntry dependentEntry, InternalEntityEntry principalEntry, IForeignKey foreignKey)
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.NavigationFixer.NavigationCollectionChanged(InternalEntityEntry entry, INavigationBase navigationBase, IEnumerable`1 added, IEnumerable`1 removed)
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.InternalEntityEntryNotifier.NavigationCollectionChanged(InternalEntityEntry entry, INavigationBase navigationBase, IEnumerable`1 added, IEnumerable`1 removed)
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.ChangeDetector.DetectNavigationChange(InternalEntityEntry entry, INavigationBase navigationBase)
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.ChangeDetector.LocalDetectChanges(InternalEntityEntry entry)
   at Microsoft.EntityFrameworkCore.ChangeTracking.Internal.ChangeDetector.DetectChanges(IStateManager stateManager)
   at Microsoft.EntityFrameworkCore.ChangeTracking.ChangeTracker.DetectChanges()
   at Microsoft.EntityFrameworkCore.DbContext.TryDetectChanges()
   at Microsoft.EntityFrameworkCore.DbContext.SaveChangesAsync(Boolean acceptAllChangesOnSuccess, CancellationToken cancellationToken)
   at CommanCenter.API.Infrastructure.Repositories.Repository`1.SaveChangesAsync() in C:\Users\AROBLEDO\source\repos\CommanCenter.API\Infrastructure\Repositories\Repository.cs:line 49
   at CommanCenter.API.Application.Services.ConsultorService.ActualizarAsync(Int32 id, ActualizarConsultorDto dto, String usuarioId) in C:\Users\AROBLEDO\source\repos\CommanCenter.API\Application\Services\ConsultorService.cs:line 204
   at CommanCenter.API.Controllers.ConsultoresController.Actualizar(Int32 id, ActualizarConsultorDto dto) in C:\Users\AROBLEDO\source\repos\CommanCenter.API\Controllers\ConsultoresController.cs:line 85
   at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.TaskOfIActionResultExecutor.Execute(ActionContext actionContext, IActionResultTypeMapper mapper, ObjectMethodExecutor executor, Object controller, Object[] arguments)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.<InvokeActionMethodAsync>g__Awaited|12_0(ControllerActionInvoker invoker, ValueTask`1 actionResultValueTask)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.<InvokeNextActionFilterAsync>g__Awaited|10_0(ControllerActionInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow(ActionExecutedContextSealed context)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State& next, Scope& scope, Object& state, Boolean& isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.<InvokeInnerFilterAsync>g__Awaited|13_0(ControllerActionInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.<InvokeFilterPipelineAsync>g__Awaited|20_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.<InvokeAsync>g__Logged|17_1(ResourceInvoker invoker)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.<InvokeAsync>g__Logged|17_1(ResourceInvoker invoker)
   at Microsoft.AspNetCore.Routing.EndpointMiddleware.<Invoke>g__AwaitRequestTask|7_0(Endpoint endpoint, Task requestTask, ILogger logger)
   at Program.<>c.<<<Main>$>b__0_2>d.MoveNext() in C:\Users\AROBLEDO\source\repos\CommanCenter.API\Program.cs:line 92
--- End of stack trace from previous location ---
   at Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext context)
   at Microsoft.AspNetCore.Authentication.AuthenticationMiddleware.Invoke(HttpContext context)
   at Serilog.AspNetCore.RequestLoggingMiddleware.Invoke(HttpContext httpContext)
   at Swashbuckle.AspNetCore.SwaggerUI.SwaggerUIMiddleware.Invoke(HttpContext httpContext)
   at Swashbuckle.AspNetCore.Swagger.SwaggerMiddleware.Invoke(HttpContext httpContext, ISwaggerProvider swaggerProvider)
   at CommanCenter.API.Middleware.ExceptionHandlerMiddleware.InvokeAsync(HttpContext context) in C:\Users\AROBLEDO\source\repos\CommanCenter.API\Middleware\ExceptionHandlerMiddleware.cs:line 25
